document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const jobDesc = document.getElementById("jobDesc").value;
  const output = document.getElementById("output");
  output.textContent = "Analyzing... please wait.";

  const formData = new FormData();
  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  }
  formData.append("job_description", jobDesc);

  const resp = await fetch("https://YOUR_RENDER_BACKEND_URL/analyze", {
    method: "POST",
    body: formData,
  });

  const data = await resp.json();
  output.textContent = JSON.stringify(data, null, 2);
});
