function gen() {
  document.getElementById('result').textContent = crypto.randomUUID();
}
function copy() {
  const el = document.getElementById('result');
  navigator.clipboard.writeText(el.textContent);
}
gen();
