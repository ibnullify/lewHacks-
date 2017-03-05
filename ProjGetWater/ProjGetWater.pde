boolean start = false;
boolean playing = false;
boolean end = false;

void setup(){
  //initial setup and anytime the game is played again  
  

}

void draw(){
  if ( start ) {
     playing = false;
     setup();
     return;
  }
  if ( playing ) {
     playGame();
     return;
  }
  if ( end ) {
     playing = false;
     endGame();
     return;
  } 
}

void playGame(){
 //this is the actual game 
}

void endGame() {
  //this is when the game is over 
}