// Handle upvotes/downvotes
document.addEventListener('click', async (e) => {
    if (!e.target.classList.contains('vote')) return;
    
    const voteBtn = e.target;
    const container = voteBtn.closest('.vote-buttons');
    const scoreSpan = container.querySelector('.score');
    const type = container.dataset.type;
    const id = container.dataset.id;
    const value = voteBtn.classList.contains('upvote') ? "up" : "down";
    
    try {
        const response = await fetch(`/vote/${type}/${id}/${value}`, { method: 'POST' });
        
        if (response.status === 401) {
            // User is not authenticated
            alert('Please log in to vote');
            // Optionally redirect to login page
            // window.location.href = '/login';
            return;
        }
        
        if (response.ok) {
            const newScore = Number(await response.text());
            scoreSpan.textContent = newScore;
        }
    } catch (error) {
        console.error('Error voting:', error);
    }
});
