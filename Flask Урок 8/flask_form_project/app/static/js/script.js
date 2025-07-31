const colorInput = document.getElementById('color');
const preview = document.getElementById('colorPreview');

colorInput.addEventListener('input', function() {
    preview.style.backgroundColor = colorInput.value;
});

const funButton = document.getElementById('funButton');
const funMessage = document.getElementById('funMessage');

funButton.addEventListener('click', () => {
    funMessage.textContent = "🎉 Поздравляю! Ты нажал на меня и теперь всё стало веселее! 🦄✨";
    const newElem = document.createElement('p');
    newElem.textContent = "Вот тебе бонус: улыбайся чаще! 😊";
    funMessage.appendChild(newElem);
});
