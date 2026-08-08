function togglePassword(fieldId, toggleEl) {
    const field = document.getElementById(fieldId);
    if (!field) return;

    if (field.type === 'password') {
        field.type = 'text';
        toggleEl.textContent = 'Hide';
    } else {
        field.type = 'password';
        toggleEl.textContent = 'Show';
    }
}