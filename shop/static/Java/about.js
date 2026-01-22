window.onload = function () {
  const paragraphs = document.querySelectorAll("p");
  paragraphs.forEach((p, i) => {
    setTimeout(() => {
      p.style.opacity = "1";
      p.style.transition = "opacity 1s";
    }, i * 1000);
  });
};
