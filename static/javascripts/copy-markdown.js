// Copies the markdown source of the current page to the clipboard, so a reader
// working alongside an AI tool can paste the source rather than text scraped
// out of the rendered page. The .md files sit next to the HTML in the build.

const RESET_AFTER_MS = 2000;

// The async clipboard API needs a secure context and a focused document, so it
// is unavailable over plain http and inside some embedded browsers. The
// textarea fallback works wherever a click handler runs.
async function writeToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    const copied = document.execCommand("copy");
    document.body.removeChild(textarea);
    return copied;
  }
}

document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-md-copy-markdown]");
  if (!button) {
    return;
  }

  const url = button.getAttribute("data-md-copy-markdown");
  let state = "data-md-copied";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`${response.status} for ${url}`);
    }
    if (!(await writeToClipboard(await response.text()))) {
      throw new Error("clipboard write refused");
    }
  } catch (error) {
    // The link beside this button opens the same markdown, so a reader who
    // hits this still has a way through.
    console.error("Could not copy the markdown source", error);
    state = "data-md-copy-failed";
  }

  button.setAttribute(state, "");
  setTimeout(() => button.removeAttribute(state), RESET_AFTER_MS);
});
