function resetVoting() {
    const confirmation = confirm("Are you sure you want to reset and start a new vote?");
    if (confirmation) {
        fetch('/reset', {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                alert("Voting has been reset!");
                window.location.reload();
            } else {
                alert("Error resetting the voting system.");
            }
        });
    }
}
