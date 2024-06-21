const POST_SUMMARIZER_TEXT_URL = "http://localhost:8000/api/summarizers/text";
const GET_SUMMARIZERS_URL = "http://localhost:8000/api/summarizers";

const form = document.querySelector("form");
const refreshSummarizersBtn = document.querySelector("#refresh-summarizers");
const summaryTextarea = document.querySelector("#summary");
const supportedSummarizers = document.querySelector("select");

function onPostSummarizerTextResult(json) {
  const { summary } = json;
  summaryTextarea.value = summary.join("\n");
}

function onGetSummarizersResult(json) {
  const { summarizers } = json;
  supportedSummarizers.replaceChildren(
    ...summarizers.map((summ) => {
      const optionElem = document.createElement("option");
      optionElem.value = summ.code;
      optionElem.innerText = summ.name;
      return optionElem;
    }),
  );
}

function getSupportedSummarizers() {
  refreshSummarizersBtn.disabled = true;
  supportedSummarizers.disabled = true;
  fetch(GET_SUMMARIZERS_URL, {})
    .then((res) => {
      if (res.ok) return res.json();
      throw new Error("Failed to get supported summarizers");
    })
    .then(onGetSummarizersResult)
    .finally(() => {
      supportedSummarizers.disabled = false;
      refreshSummarizersBtn.disabled = false;
    });
}

function onSummarizeText(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const content = formData.get("content");
  const rows = parseInt(formData.get("rows"));
  const summarizer = formData.get("summarizer");
  const language = formData.get("language");

  fetch(POST_SUMMARIZER_TEXT_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content, summarizer, rows, language }),
  })
    .then((res) => {
      if (res.ok) return res.json();
      throw new Error("Failed to post summarizer text");
    })
    .then(onPostSummarizerTextResult);
}

// On start
form.addEventListener("submit", onSummarizeText);
refreshSummarizersBtn.addEventListener("click", getSupportedSummarizers);
getSupportedSummarizers();
