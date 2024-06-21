const POST_SUMMARIZER_TEXT_URL = "http://localhost:8000/api/summarizers/text";
const GET_SUMMARIZERS_URL = "http://localhost:8000/api/summarizers";

const form = document.querySelector("form");
const formSubmitBtn = document.querySelector("form input[type=submit]");
const refreshSummarizersBtn = document.querySelector("#refresh-summarizers");
const summaryTextarea = document.querySelector("#summary");
const supportedSummarizers = document.querySelector("select");

function changeLoadingState(domElem, state) {
  // Changes the Bulma CSS library skeleton property
  if (state === false) {
    domElem.classList.remove("is-skeleton");
    domElem.disabled = false;
    return;
  }
  if (state === true) {
    domElem.classList.add("is-skeleton");
    domElem.disabled = true;
    return;
  }
}

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
  changeLoadingState(supportedSummarizers, true);
  changeLoadingState(refreshSummarizersBtn, true);
  fetch(GET_SUMMARIZERS_URL, {})
    .then((res) => {
      if (res.ok) return res.json();
      throw new Error("Failed to get supported summarizers");
    })
    .then(onGetSummarizersResult)
    .finally(() => {
      changeLoadingState(supportedSummarizers, false);
      changeLoadingState(refreshSummarizersBtn, false);
    });
}

function onSummarizeText(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const content = formData.get("content");
  const rows = parseInt(formData.get("rows"));
  const summarizer = formData.get("summarizer");
  const language = formData.get("language");

  changeLoadingState(summaryTextarea, true);
  changeLoadingState(formSubmitBtn, true);
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
    .then(onPostSummarizerTextResult)
    .finally(() => {
      changeLoadingState(summaryTextarea, false);
      changeLoadingState(formSubmitBtn, false);
    });
}

// On start
form.addEventListener("submit", onSummarizeText);
refreshSummarizersBtn.addEventListener("click", getSupportedSummarizers);
getSupportedSummarizers();
