<!DOCTYPE html>
 
 <html>
 <head>

<title>
    Henrieke
</title>

</head>


<meta charset="utf-8"/>


<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="stylesheet" href="style.css" type="text/css">

<script src="js/jquery/jquery.js">
</script>
<script src="js/graphic.js">
</script>
<script src="js/player.js">
</script>
<script src="js/game.js">
</script>
<script src="js/request.js">
</script>
<body>

<script>
    let game = new Game(1);
    // game.addPlayer("Peter1", 1, );
    // game.addPlayer("Peter2", 2);
    // game.addPlayer("Peter3", 3);
    // game.addPlayer("Peter4", 4);
    game.setupGraphic();
    
    // game.request.createGame();
    // game.request.startGame(11);
    // game.request
    // game.request.createGame(2);
    // game.request.joinGame(2, "sophia");
    // game.request.joinGame(2, "regina");
    // game.request.startGame(2);
    // game.request.playCard(2, 1, 2);
    // game.request.playCard(2, 2, 3);
    // game.request.playCard(2, 3, 9);
    // game.request.playCard(2, 4, 1);
    // game.request.getCards(2);
</script>

<?php
require 'php/computeronly/game.php';

// function playComputer() {
//     $game = new Game();
//     $game->addPlayer("bea", "beaBot");
//     $game->addPlayer("niklas", "niklasBot");
//     $game->addPlayer("henrieke", "henriekeBot");
//     $game->addPlayer("ausweglos", "ausweglosBot");
//     $game->addPlayer("random", "randomBot");
//     $game->start();
// }
// playComputer();
?>


</body>
</html>
