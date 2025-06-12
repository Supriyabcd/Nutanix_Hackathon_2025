console.log("Main.js is loaded!");

function getCSRFToken() {
  const token = document.querySelector("[name=csrf-token]");
  return token ? token.content : "";
}

document.addEventListener("DOMContentLoaded", () => {
  const preview = document.getElementById("preview");
  const reviewBtn = document.getElementById("review-btn");
  const languageSelect = document.getElementById("language-select");

  const editor = ace.edit("code-editor");
  editor.setTheme("ace/theme/monokai");
  editor.session.setMode("ace/mode/python"); // default to python
  editor.setOptions({
    fontSize: "14px",
    showPrintMargin: false,
    wrap: true,
  });

  languageSelect.addEventListener("change", function () {
    const langMap = {
      c: "c_cpp",
      cpp: "c_cpp",
      python: "python",
      ruby: "ruby",
      java: "java",
      javascript: "javascript",
      php: "php",
      csharp: "csharp",
    };
    const mode = langMap[this.value] || "text";
    editor.session.setMode(`ace/mode/${mode}`);
  });

  reviewBtn.addEventListener("click", async () => {
    const code = editor.getValue();
    const language = languageSelect.value;

    console.log("Code to send:", code);

    const dataToSave = {
      code: code,
      language: language,
      timestamp: new Date().toISOString(),
    };
    localStorage.setItem("codeReviewSubmission", JSON.stringify(dataToSave));

    preview.innerText = " Reviewing your code...";

    try {
      const response = await fetch("/ask-gemini/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          prompt: `Please review the following ${language} code:\n${code}`,
        }),
      });

      const data = await response.json();
      console.log("Full response data:", data);

      if (response.ok && data.reply) {
        preview.innerText = `\n\n${data.reply}`;
      } else {
        preview.innerText = ` Error: ${
          data.error || "Unknown error"
        }\nDetails: ${data.details || "No extra details"}`;
      }
    } catch (err) {
      console.error("Gemini fetch error:", err);
      preview.innerText = "Failed to connect to Gemini API.";
    }
  });
});
