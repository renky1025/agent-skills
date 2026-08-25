const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  const htmlPath = args[0];
  const outputPath = args[1];
  const width = parseInt(args[2]) || 1200;
  const height = parseInt(args[3]) || 1600;
  const fullpage = args[4] === 'fullpage';
  const scale = parseFloat(args[5]) || 2; // DPR/scale factor for quality

  if (!htmlPath || !outputPath) {
    console.error('Usage: node capture.js <html> <png> [width] [height] [fullpage] [scale]');
    process.exit(1);
  }

  let chromium;
  try {
    const { createRequire } = require('module');
    const req = createRequire(__filename);
    chromium = req('playwright').chromium;
  } catch {
    console.error('Playwright not found. Run: cd ~/.workbuddy/skills/infocard && npm install && npx playwright install chromium');
    process.exit(1);
  }

  const fs = require('fs');
  const cached = '/Users/kyren/Library/Caches/ms-playwright';
  let execPath = null;
  if (!process.env.PLAYWRIGHT_BROWSERS_PATH) {
    // try headless shell versions in descending order
    const entries = fs.readdirSync(cached).filter(e => e.startsWith('chromium_headless_shell-')).sort().reverse();
    for (const e of entries) {
      const p = path.join(cached, e, 'chrome-headless-shell-mac-arm64', 'chrome-headless-shell');
      if (fs.existsSync(p)) { execPath = p; break; }
    }
    if (!execPath) {
      // fallback: try full chromium
      const cEntries = fs.readdirSync(cached).filter(e => e.startsWith('chromium-')).sort().reverse();
      for (const e of cEntries) {
        const p = path.join(cached, e, 'chrome-mac-arm64', 'Google Chrome for Testing.app', 'Contents', 'MacOS', 'Google Chrome for Testing');
        if (fs.existsSync(p)) { execPath = p; break; }
      }
    }
  }

  const browser = await chromium.launch({ executablePath: execPath });
  const context = await browser.newContext({ deviceScaleFactor: scale });
  const page = await context.newPage();

  if (fullpage) {
    // Step 1: load at wide viewport so content flows naturally
    await page.setViewportSize({ width: width, height: 3000 });
    const fileUrl = 'file://' + path.resolve(htmlPath);
    await page.goto(fileUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // Step 2: neutralize ALL centering/100vh layouts — force body to top-left flow
    // This is the key fix: strip every style that causes vertical centering
    await page.evaluate(() => {
      const html = document.documentElement;
      const body = document.body;

      // Strip body inline styles and computed styles that center content
      const bodyStyle = body.style;
      bodyStyle.setProperty('display', 'block', 'important');
      bodyStyle.setProperty('min-height', 'auto', 'important');
      bodyStyle.setProperty('height', 'auto', 'important');
      bodyStyle.setProperty('align-items', 'normal', 'important');
      bodyStyle.setProperty('justify-content', 'normal', 'important');
      bodyStyle.setProperty('margin-top', '0px', 'important');
      bodyStyle.setProperty('padding-top', '0px', 'important');
      bodyStyle.setProperty('margin', '0', 'important');
      bodyStyle.setProperty('padding', '0', 'important');

      // Strip html too
      const htmlStyle = html.style;
      htmlStyle.setProperty('min-height', 'auto', 'important');

      // Force reflow so the card snaps to top
      void body.offsetHeight;
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(300);

    // Step 3: measure card at top of viewport
    const cardInfo = await page.evaluate(() => {
      const el = document.querySelector('.card') ||
                 document.querySelector('.container') ||
                 document.body.children[0];
      if (!el) return null;
      const rect = el.getBoundingClientRect();
      return {
        left: rect.left,
        top: rect.top,
        width: rect.width,
        height: rect.height,
      };
    });

    if (cardInfo && cardInfo.width > 50 && cardInfo.height > 50) {
      // Step 4: viewport = exactly card bounds — no padding, no clip, no letterboxing
      // card.top should now be ~0, so viewport from 0 to card bottom = pure card image
      const vpW = Math.max(1, Math.ceil(cardInfo.width));
      const vpH = Math.max(1, Math.ceil(cardInfo.top) + Math.ceil(cardInfo.height));
      await page.setViewportSize({ width: vpW, height: vpH });
      await page.waitForTimeout(200);

      await page.screenshot({
        path: path.resolve(outputPath),
        type: 'png',
        fullPage: false,
      });
    } else {
      // fallback
      const bounds = await page.evaluate(() => ({
        w: Math.max(document.body.scrollWidth, document.documentElement.scrollWidth),
        h: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
      }));
      await page.setViewportSize({ width, height: bounds.h });
      await page.screenshot({ path: path.resolve(outputPath), type: 'png', fullPage: true });
    }
  } else {
    await page.setViewportSize({ width, height });
    const fileUrl = 'file://' + path.resolve(htmlPath);
    await page.goto(fileUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    await page.evaluate(() => {
      const body = document.body;
      const bodyStyle = body.style;
      bodyStyle.setProperty('display', 'block', 'important');
      bodyStyle.setProperty('min-height', 'auto', 'important');
      bodyStyle.setProperty('height', 'auto', 'important');
      bodyStyle.setProperty('align-items', 'normal', 'important');
      bodyStyle.setProperty('justify-content', 'normal', 'important');
      bodyStyle.setProperty('margin', '0', 'important');
      bodyStyle.setProperty('padding', '0', 'important');
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(200);

    const cardInfo = await page.evaluate(() => {
      const el = document.querySelector('.card') ||
                 document.querySelector('.container') ||
                 document.body.children[0];
      if (!el) return null;
      const rect = el.getBoundingClientRect();
      return { top: rect.top, left: rect.left, width: rect.width, height: rect.height };
    });

    if (cardInfo && cardInfo.width > 50 && cardInfo.height > 50) {
      const vpW = Math.max(1, Math.ceil(cardInfo.width));
      const vpH = Math.max(1, Math.ceil(cardInfo.top) + Math.ceil(cardInfo.height));
      await page.setViewportSize({ width: vpW, height: vpH });
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.resolve(outputPath), type: 'png', fullPage: false });
    } else {
      await page.screenshot({ path: path.resolve(outputPath), type: 'png', fullPage: false });
    }
  }

  await browser.close();
  console.log('OK: ' + path.resolve(outputPath));
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});