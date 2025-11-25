// Planche de Galton

let balls = [];
let gridSize = 10
let counts = [];
let maxBalls = 2000;
let deadBalls = [];

function setup() {
  createCanvas(200, 400);
  //frameRate(10);
  for (i = 0; i < width / gridSize - 1 ; i++) {
    counts[i] = 0;
  }  
}

function draw() {
  background(237, 221, 183);
  
  displayBoard();
  
  //création des billes
  if (frameCount < maxBalls * 2 && frameCount % 2 == 0) {
    balls.push(new Ball());
  }
  
  //dessin des billes
  for (let ball of balls) {
    ball.move();
    ball.display();
  }
  
  // dessin des barres
  displayBars();
  
  // Supression des billes mortes
  for (let ball of deadBalls) {
    balls.splice(balls.indexOf(ball), 1);
  }
  deadBalls = [];
}

function displayBoard() {
  //dessin des points de la grille
  push();
  noStroke();
  fill(100);
  for (let x = 0; x <= width ; x += gridSize) {
    for (let y = gridSize ; y < width; y += gridSize) {
      let xo = (y % (gridSize * 2) == 0) ? x - gridSize/2 : x;
      circle(xo, y, 2);
    }
  }
  //dessin des couloirs  
  stroke(100);
  for (let x = gridSize / 2; x < width; x += gridSize) {
    line(x, width, x, height);
  }
  pop();
}

function displayBars() {
  push();
  strokeCap(ROUND);
  stroke('blue');
  strokeWeight(gridSize/3+1);
  for (let i = 0; i < counts.length; i++) {
    let x = (i + 1) * gridSize
    let y = height - (counts[i] / 2) + (gridSize / 4)
    line(x , height + gridSize / 4, x, y);
  }
  pop();
  
}

class Ball {
  constructor() {
    this.x = width / 2 ;
    this.y = 0;
    this.jig = true;
  }

  move() {
      this.y += gridSize / 2;
      if (this.jig) {
        if (this.y % gridSize == 0) {
          this.x += random([-gridSize / 2, gridSize / 2]);
        }
      } 
      let column = int((this.x - gridSize / 2) / gridSize);
      if (this.y > width) {
        this.jig = false;
        if (this.y >= height - counts[column] / 2) {
          deadBalls.push(this);
          counts[column] += 1;
        }
      }
  }
  
  display() {
    push()
    noStroke();
    fill("blue");
    circle(this.x, this.y, gridSize/3 +1);
    pop();
  }
}