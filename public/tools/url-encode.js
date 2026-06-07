function encode() {
  const v = document.getElementById('inp').value;
  document.getElementById('out').value = encodeURIComponent(v);
}
function decode() {
  try {
    const v = document.getElementById('inp').value;
    document.getElementById('out').value = decodeURIComponent(v);
  } catch (_) {
    document.getElementById('out').value = '解码失败：输入不是有效的 URL 编码';
  }
}
