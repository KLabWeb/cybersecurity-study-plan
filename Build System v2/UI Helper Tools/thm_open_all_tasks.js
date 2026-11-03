// thm_open_all_tasks.js
// Paste into the browser console on a TryHackMe room page, press Enter, wait for "DONE", then save the page.
// It changes only what YOUR browser shows. It sends nothing anywhere and reads no cookies or tokens.
//
// What it does:
//   1. Finds every task panel on the page (the regions whose id starts with "content-").
//   2. Forces each one to stay visible, even though the site closes a task when you open the next one.
//   3. If a task's text is not loaded yet, it opens that task once, waits, and keeps a copy of its text on the page.
//   4. Prints a word count per task so you can see nothing is empty.

(async function openAllTasks() {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const wordCount = (element) => (element.innerText || element.textContent || "").trim().split(/\s+/).filter(Boolean).length;

  // Keep a panel visible no matter what the site's own styles say.
  function forceVisible(element) {
    element.removeAttribute("hidden");
    element.setAttribute("aria-hidden", "false");
    const style = element.style;
    style.setProperty("display", "block", "important");
    style.setProperty("visibility", "visible", "important");
    style.setProperty("opacity", "1", "important");
    style.setProperty("height", "auto", "important");
    style.setProperty("max-height", "none", "important");
    style.setProperty("overflow", "visible", "important");
  }

  const headers = Array.from(document.querySelectorAll('button[id^="header-"]'));
  if (headers.length === 0) {
    console.warn("No task headers found. Is this a room page, and has it finished loading?");
    return;
  }
  console.log("Found " + headers.length + " tasks.");

  // Pass 1: open any task whose text is not in the page yet, and keep a copy of it.
  for (const header of headers) {
    const taskNumber = header.id.replace("header-", "");
    let panel = document.getElementById("content-" + taskNumber);

    if (!panel || wordCount(panel) < 20) {
      header.scrollIntoView({ block: "center" });
      if (header.getAttribute("aria-expanded") !== "true") {
        header.click();
      }
      // Wait up to 8 seconds for the task text to arrive.
      for (let tries = 0; tries < 16; tries++) {
        await sleep(500);
        panel = document.getElementById("content-" + taskNumber);
        if (panel && wordCount(panel) >= 20) break;
      }
      if (panel && wordCount(panel) >= 20) {
        // Keep a copy that the site will not remove when the next task opens.
        const copy = panel.cloneNode(true);
        copy.id = "saved-copy-content-" + taskNumber;
        copy.setAttribute("data-saved-copy", "true");
        forceVisible(copy);
        const label = document.createElement("h3");
        label.textContent = "SAVED COPY OF " + (header.innerText || "Task " + taskNumber).trim();
        const holder = document.createElement("div");
        holder.setAttribute("data-saved-copy-holder", taskNumber);
        holder.style.cssText = "border:2px dashed #888;margin:16px 0;padding:12px;";
        holder.appendChild(label);
        holder.appendChild(copy);
        header.closest("h3, div").parentElement.appendChild(holder);
      }
    }
  }

  // Pass 2: force every real panel, and the wrappers around it, to stay visible.
  for (const header of headers) {
    const taskNumber = header.id.replace("header-", "");
    const panel = document.getElementById("content-" + taskNumber);
    if (!panel) continue;
    forceVisible(panel);
    // The site collapses a task by shrinking a wrapper, so open up to three wrappers above the panel too.
    let wrapper = panel.parentElement;
    for (let depth = 0; wrapper && depth < 3; depth++) {
      if (wrapper.querySelector('button[id^="header-"]') && wrapper.querySelectorAll('button[id^="header-"]').length > 1) break;
      forceVisible(wrapper);
      wrapper = wrapper.parentElement;
    }
    header.setAttribute("aria-expanded", "true");
  }

  // Report.
  let emptyTasks = 0;
  for (const header of headers) {
    const taskNumber = header.id.replace("header-", "");
    const panel = document.getElementById("content-" + taskNumber);
    const copy = document.getElementById("saved-copy-content-" + taskNumber);
    const words = Math.max(panel ? wordCount(panel) : 0, copy ? wordCount(copy) : 0);
    if (words < 20) emptyTasks++;
    console.log("Task " + taskNumber + ": " + words + " words" + (words < 20 ? "   <-- EMPTY, open this task by hand and run the script again" : ""));
  }
  window.scrollTo(0, 0);
  console.log(emptyTasks === 0 ? "DONE. All tasks are open. Save the page now." : "DONE, but " + emptyTasks + " task(s) are empty. See the lines above.");
})();
