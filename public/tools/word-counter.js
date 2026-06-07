function count() {
  const t = document.getElementById('inp').value;
  document.getElementById('chars').textContent = t.length;
  document.getElementById('words').textContent = (t.match(/\S+/g) || []).length;
  document.getElementById('lines').textContent = t.split('\n').length;
  document.getElementById('cn').textContent = (t.match(/[\u4e00-\u9fff]/g) || []).length;
}
