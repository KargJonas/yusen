
// Handle upvotes/downvotes
document.addEventListener('click', async (e) => {
    if (!e.target.classList.contains('vote')) return;
    
    const voteBtn = e.target;
    const container = voteBtn.closest('.vote-buttons');
    const scoreSpan = container.querySelector('.score');
    const type = container.dataset.type;
    const id = container.dataset.id;
    const value = voteBtn.classList.contains('upvote') ? 1 : -1;
    
    try {
        const response = await fetch(`/vote/${type}/${id}/${value}`, { method: 'POST' });

        // Update interface with new upvote count
        if (response.ok) {
            const newScore = await response.text();
            scoreSpan.textContent = newScore;
        }
    } catch (error) {
        console.error('Error voting:', error);
    }
});
