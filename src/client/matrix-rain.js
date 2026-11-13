const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const matrix = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴ日月火水木金土人山川田中本大小愛恨心神夢現実未来時空世界宇宙龍鳳";
const baseFontSize = 18;

// Each column gets depth, speed, and max length
const columnsData = Array(Math.floor(canvas.width / baseFontSize)).fill().map(() => {
  const depth = Math.random(); // 0 = front (fast, big, bright), 1 = far (slow, small, dim)
  return {
    y: Math.random() * -canvas.height,
    depth: depth,
    speed: 0.3 + (1 - depth) * 2.2,           // far = very slow (0.3), close = fast (2.5)
    maxLength: 8 + Math.floor((1 - depth) * 35), // close = longer trails
  };
});

function draw() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.09)';   // gentle but visible fade
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < columnsData.length; i++) {
    const col = columnsData[i];

    // Depth-based appearance
    const fontSize = baseFontSize * (1 - col.depth * 0.7); // far = up to 70% smaller
    const opacity = 0.3 + (1 - col.depth) * 0.7;           // far = dimmer (0.3), close = bright (1.0)
    const green = Math.floor(140 + (1 - col.depth) * 115); // far = darker green (140), close = vivid (255)

    const text = matrix[Math.floor(Math.random() * matrix.length)];
    const x = i * baseFontSize;
    const y = col.y * baseFontSize;

    // Very rare white flash — only on closer streams (depth < ~0.7)
    const whiteChance = 0.003 * (1 - col.depth); // ~0.3% max, almost zero on distant streams
    if (Math.random() < whiteChance) {
      ctx.fillStyle = '#ffffff';
      ctx.font = fontSize + 'px monospace';
      ctx.fillText(text, x, y);
      ctx.fillStyle = `rgba(0, ${green}, 0, ${opacity})`;  // reset to pure green
    } else {
      ctx.fillStyle = `rgba(0, ${green}, 0, ${opacity})`;  // pure green, no red/blue
      ctx.font = fontSize + 'px monospace';
      ctx.fillText(text, x, y);
    }

    // Fading trail (also pure green, depth-affected)
    if (col.y > 0) {
      for (let j = 1; j < col.maxLength; j++) {
        if (y - j * baseFontSize > 0) {
          const trailOpacity = opacity * (1 - j / col.maxLength) * 0.6;
          ctx.fillStyle = `rgba(0, ${green}, 0, ${trailOpacity})`;  // pure green trail
          ctx.font = (fontSize * (1 - j / col.maxLength * 0.6)) + 'px monospace';
          ctx.fillText(
            matrix[Math.floor(Math.random() * matrix.length)],
            x,
            y - j * baseFontSize
          );
        }
      }
    }

    // Move — parallax: farther = much slower
    col.y += col.speed;

    // Reset
    if (y > canvas.height) {
      col.y = Math.random() * -80;
      col.depth = Math.random();
      col.speed = 0.3 + (1 - col.depth) * 2.2;
      col.maxLength = 8 + Math.floor((1 - col.depth) * 35);
    }
  }
}

setInterval(draw, 35);

window.addEventListener('resize', () => {
  canvas.height = window.innerHeight;
  canvas.width = window.innerWidth;
});
