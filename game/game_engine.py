import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)

        # Attempt tracking
        self.attempts = 0
        self.max_attempts = 10

        # Dynamic search range
        self.min_range = 1
        self.max_range = 100

        # Recent guess history
        self.guess_history = []

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False
        self.game_over = False

        self.input_box = TextBox(width // 2 - 110, 150, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 150, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):
        # Do not accept guesses after the game has ended.
        if self.game_won or self.game_over:
            return

        # Prevent crashes when the input box is empty.
        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number!"
            self.feedback_color = (240, 200, 80)
            return

        guess = int(self.input_box.text)

        # A valid guess consumes one attempt.
        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)

            # The secret number must be greater than the guess.
            self.min_range = max(self.min_range, guess + 1)

            # Add guess to history.
            self.guess_history.append(
                (guess, "TOO LOW", (80, 160, 240))
            )

        elif guess > self.secret_number:
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)

            # The secret number must be smaller than the guess.
            self.max_range = min(self.max_range, guess - 1)

            # Add guess to history.
            self.guess_history.append(
                (guess, "TOO HIGH", (240, 100, 80))
            )

        else:
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.game_won = True

            # Add correct guess to history.
            self.guess_history.append(
                (guess, "CORRECT", (80, 220, 90))
            )

            return

        # If the player has used all attempts without guessing correctly,
        # end the game and reveal the secret number.
        if self.attempts >= self.max_attempts:
            self.feedback_msg = (
                f"GAME OVER! The secret number was {self.secret_number}."
            )
            self.feedback_color = (240, 100, 80)
            self.game_over = True

    def reset(self):
        self.secret_number = random.randint(1, 100)

        # Reset attempts.
        self.attempts = 0

        # Reset dynamic range.
        self.min_range = 1
        self.max_range = 100

        # Reset guess history.
        self.guess_history = []

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False
        self.game_over = False

        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()

            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        # Title
        title_surf = self.font_title.render(
            "Number Guessing Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                35
            )
        )

        # Attempts
        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts} / {self.max_attempts}",
            True,
            (180, 185, 195)
        )

        screen.blit(
            attempts_surf,
            (
                self.width // 2 - attempts_surf.get_width() // 2,
                95
            )
        )

        # Input box
        self.input_box.render(screen)

        # Submit button
        pygame.draw.rect(
            screen,
            (50, 150, 80),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx - btn_text.get_width() // 2,
                self.submit_btn.centery - btn_text.get_height() // 2
            )
        )

        # Feedback
        feedback_surf = self.font_medium.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2 - feedback_surf.get_width() // 2,
                235
            )
        )

        # Dynamic search range
        range_surf = self.font_medium.render(
            f"Valid Range: {self.min_range} - {self.max_range}",
            True,
            (200, 205, 215)
        )

        screen.blit(
            range_surf,
            (
                self.width // 2 - range_surf.get_width() // 2,
                275
            )
        )

        # Recent guess history
        history_title = self.font_medium.render(
            "Recent Guesses",
            True,
            (245, 245, 245)
        )

        screen.blit(
            history_title,
            (
                self.width // 2 - history_title.get_width() // 2,
                315
            )
        )

        # Show only the five most recent guesses.
        recent_guesses = self.guess_history[-5:]

        start_y = 350

        for index, (guess, result, color) in enumerate(recent_guesses):
            history_text = f"{guess}  →  {result}"

            history_surf = self.font_small.render(
                history_text,
                True,
                color
            )

            screen.blit(
                history_surf,
                (
                    self.width // 2 - history_surf.get_width() // 2,
                    start_y + index * 27
                )
            )

        # Restart message after winning or losing.
        if self.game_won or self.game_over:
            restart_y = start_y + len(recent_guesses) * 27 + 20

            restart_surf = self.font_medium.render(
                "Press [R] to Start a New Game",
                True,
                (255, 220, 80)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    restart_y
                )
            )