async function fetchRecommendations(){
  const uid = document.getElementById("userId").value || 1;
  const res = await fetch(`http://localhost:8000/recommend/${uid}`);
  if(!res.ok){
    document.getElementById("results").innerText = "API error: " + res.statusText;
    return;
  }
  const data = await res.json();
  const container = document.getElementById("results");
  container.innerHTML = "";
  if(data.length === 0){
    container.innerText = "No recommendations available. Seed the DB and ensure the backend is running.";
    return;
  }
  data.forEach(item => {
    const div = document.createElement("div");
    div.className = "product";
    const img = document.createElement("img");
    img.src = item.product.image_url || "https://via.placeholder.com/100";
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.innerHTML = `<div><strong>${item.product.title}</strong> — $${item.product.price}</div>
                      <div class="score">score: ${item.score.toFixed(3)}</div>
                      <div>${item.explanation}</div>`;
    div.appendChild(img);
    div.appendChild(meta);
    container.appendChild(div);
  });
}
