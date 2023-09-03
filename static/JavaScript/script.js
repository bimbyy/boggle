document.addEventListener("DOMContentLoaded", function() {
    //setting the variables to be used
    const form = document.getElementById("guess-form");
    const resultElement = document.getElementById("result"); 
    const scoreElement = document.getElementById("score");
    const timerElement = document.getElementById("timer");
    const statsElement = document.getElementById("stats"); 
    let currentScore = 0;
    let timeRemaining = 60;
    //setting up the timer function
    const timerInterval = setInterval(function() {
        if (timeRemaining > 0) {
            timeRemaining--;
            timerElement.textContent = `Time remaining: ${timeRemaining} seconds`;
        } else {
            clearInterval(timerInterval);
            form.removeEventListener("submit", submitHandler);
            timerElement.textContent = "Time's up!";
            
            // Increment the "Games Played" counter when the timer expires
            const currentGamesPlayed = parseInt(statsElement.textContent.split(":")[1].trim());
            statsElement.textContent = `Games played: ${currentGamesPlayed + 1}`;
            axios.post("/update-session", {
                games_played: currentGamesPlayed + 1,
                highest_score: currentScore,
            })
            .then(response => {
                console.log(response.data.message);
            })
            .catch(error => {
                console.error("AJAX request error:", error);
            });
        }
    }, 1000); // This is where im having issues as when I enter a word it increments the games played/

    const submitHandler = function(event) {
        event.preventDefault();
        const guessInput = document.getElementById("guess");
        const guess = guessInput.value;

        axios.post("/check-word", { guess })
            .then(response => {
                const result = response.data.result;
                if (result === "ok") {
                    resultElement.textContent = `${guess} is a valid word!`;
                    currentScore += guess.length;
                    scoreElement.textContent = `Score: ${currentScore}`;
                } else if (result === "not-on-board") {
                    resultElement.textContent = `${guess} is not present on the board.`;
                } else if (result === "not-word") {
                    resultElement.textContent = `${guess} is not a valid word.`;
                }
                // Update statistics
                statsElement.textContent = `Games played: ${response.data.n_played} | Highest score: ${response.data.highest_score}`;
            })
            .catch(error => {
                console.error("AJAX request error:", error);
            });
    };

    form.addEventListener("submit", submitHandler);
});
