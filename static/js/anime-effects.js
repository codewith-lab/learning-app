// Anime-style effects for Cat Body Language Tutorial

document.addEventListener("DOMContentLoaded", () => {
  // Add sparkle effect to buttons
  const buttons = document.querySelectorAll(".kawaii-button")

  buttons.forEach((button) => {
    button.addEventListener("mouseover", createSparkles)
  })

  function createSparkles(e) {
    const button = e.target
    const buttonRect = button.getBoundingClientRect()

    for (let i = 0; i < 5; i++) {
      const sparkle = document.createElement("div")
      sparkle.className = "sparkle"

      // Random position around the button
      const x = Math.random() * buttonRect.width
      const y = Math.random() * buttonRect.height

      sparkle.style.left = `${buttonRect.left + x}px`
      sparkle.style.top = `${buttonRect.top + y}px`
      sparkle.style.width = `${Math.random() * 10 + 5}px`
      sparkle.style.height = sparkle.style.width
      sparkle.style.backgroundColor = getRandomColor()

      document.body.appendChild(sparkle)

      // Animate and remove
      setTimeout(() => {
        sparkle.remove()
      }, 1000)
    }
  }

  function getRandomColor() {
    const colors = [
      "#ff6b6b", // Primary
      "#4ecdc4", // Secondary
      "#ffbe76", // Accent
      "#55efc4", // Success
      "#ffeaa7", // Warning
      "#74b9ff", // Info
    ]

    return colors[Math.floor(Math.random() * colors.length)]
  }

  // Add CSS for sparkles
  const style = document.createElement("style")
  style.textContent = `
        .sparkle {
            position: fixed;
            pointer-events: none;
            border-radius: 50%;
            opacity: 0;
            z-index: 9999;
            animation: sparkle 1s ease-in-out;
        }
        
        @keyframes sparkle {
            0% {
                transform: scale(0) rotate(0deg);
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                transform: scale(1.5) rotate(180deg);
                opacity: 0;
            }
        }
    `
  document.head.appendChild(style)

  // Add hover effects to cat cards
  const catCards = document.querySelectorAll(".category-card")

  catCards.forEach((card) => {
    card.addEventListener("mouseover", () => {
      const img = card.querySelector("img")
      if (img) {
        img.style.transform = "scale(1.1) rotate(5deg)"
      }
    })

    card.addEventListener("mouseout", () => {
      const img = card.querySelector("img")
      if (img) {
        img.style.transform = "scale(1)"
      }
    })
  })

  // Add meow sound to neko teacher
  const nekoTeachers = document.querySelectorAll(".neko-teacher-img")

  nekoTeachers.forEach((neko) => {
    neko.addEventListener("click", () => {
      const meow = new Audio("/static/sounds/meow.mp3")
      meow.volume = 0.5
      meow.play()

      // Add bounce animation
      neko.style.animation = "bounce 0.5s"
      setTimeout(() => {
        neko.style.animation = ""
      }, 500)
    })
  })
})
