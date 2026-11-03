// reddit_expand_all_comments.js
// Paste into the browser console on a Reddit thread page, press Enter, wait for "DONE", then save the page.
// It only clicks the same "more replies" and "view more comments" controls you could click by hand, one at a time,
// with a pause between clicks. It sends nothing anywhere and reads no cookies or tokens.
//
// Works on the current Reddit layout (www.reddit.com) and on the old layout (old.reddit.com).
// Tip: on old.reddit.com, adding the query limit=500 to the thread address loads more comments before you start.
//
// What it does:
//   1. Opens every collapsed comment.
//   2. Clicks every "more replies" / "load more comments" / "continue this thread"-style control it can find.
//   3. Repeats until a full pass finds nothing new, or until the safety limits below are hit.
//   4. Prints how many comments are on the page at the end.

(async function expandAllRedditComments() {
  const PAUSE_BETWEEN_CLICKS_MS = 900;   // keep this human-paced; lowering it risks Reddit rate-limiting your browser
  const WAIT_AFTER_PASS_MS = 2500;       // time for newly requested comments to arrive
  const MAX_CLICKS = 600;
  const MAX_PASSES = 60;

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const isOldLayout = location.hostname.startsWith("old.") || !!document.querySelector("body.comments-page .sitetable.nestedlisting");

  function countComments() {
    if (isOldLayout) return document.querySelectorAll(".comment .usertext-body").length;
    return document.querySelectorAll("shreddit-comment").length;
  }

  // Look inside open shadow roots too, because the current layout builds its buttons inside web components.
  function deepQueryAll(root, selector, found = []) {
    root.querySelectorAll(selector).forEach((el) => found.push(el));
    root.querySelectorAll("*").forEach((el) => { if (el.shadowRoot) deepQueryAll(el.shadowRoot, selector, found); });
    return found;
  }

  const LOAD_MORE_TEXT = /more repl|view more comment|load more comment|show more repl|see more repl|more comment/i;

  function findLoadMoreControls() {
    if (isOldLayout) {
      return Array.from(document.querySelectorAll(".morecomments a, .morechildren a")).filter((a) => !a.dataset.expandClicked);
    }
    const candidates = deepQueryAll(document, 'button, a, faceplate-partial[loading="action"]');
    return candidates.filter((el) => {
      if (el.dataset && el.dataset.expandClicked) return false;
      if (el.closest && el.closest("shreddit-ad-post, shreddit-comments-page-ad")) return false;
      if (el.tagName === "A" && (el.getAttribute("href") || "").indexOf("/comments/") !== -1) return false; // a link to another page, not a loader
      const label = (el.innerText || el.textContent || el.getAttribute("aria-label") || "").trim();
      return label.length < 60 && LOAD_MORE_TEXT.test(label);
    });
  }

  function openCollapsedComments() {
    let opened = 0;
    if (isOldLayout) {
      document.querySelectorAll(".comment.collapsed > .entry a.expand").forEach((a) => { a.click(); opened++; });
    } else {
      document.querySelectorAll("shreddit-comment[collapsed]").forEach((c) => { c.removeAttribute("collapsed"); opened++; });
    }
    return opened;
  }

  let layoutName = "current";
  if (isOldLayout) layoutName = "old";
  console.log("Layout: " + layoutName + ". Comments on page at start: " + countComments());

  let totalClicks = 0;
  for (let pass = 1; pass <= MAX_PASSES; pass++) {
    const opened = openCollapsedComments();
    const controls = findLoadMoreControls();
    if (controls.length === 0 && opened === 0) {
      console.log("Pass " + pass + ": nothing left to open.");
      break;
    }
    console.log("Pass " + pass + ": opened " + opened + " collapsed, clicking " + controls.length + " load-more controls...");
    for (const control of controls) {
      if (totalClicks >= MAX_CLICKS) break;
      try {
        if (control.dataset) control.dataset.expandClicked = "1";
        control.scrollIntoView({ block: "center" });
        control.click();
        totalClicks++;
      } catch (error) {
        console.warn("Could not click one control:", error);
      }
      await sleep(PAUSE_BETWEEN_CLICKS_MS);
    }
    if (totalClicks >= MAX_CLICKS) { console.warn("Stopped at the click limit (" + MAX_CLICKS + "). Run the script again to continue."); break; }
    await sleep(WAIT_AFTER_PASS_MS);
  }

  // Old layout only: "continue this thread" links lead to a separate page and cannot be opened in place. List them.
  if (isOldLayout) {
    const deepLinks = Array.from(document.querySelectorAll(".deepthread a")).map((a) => a.href);
    if (deepLinks.length) {
      console.log(deepLinks.length + ' "continue this thread" links lead to separate pages. Open and save those too if you want them:');
      deepLinks.forEach((href) => console.log("  " + href));
    }
  }

  window.scrollTo(0, 0);
  console.log("DONE. Clicks made: " + totalClicks + ". Comments on page now: " + countComments() + ". Save the page now.");
})();
