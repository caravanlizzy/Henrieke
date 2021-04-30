<!DOCTYPE html>
 
 <html>
 <head>

<title>
    Henrieke
</title>

</head>


<meta charset="utf-8"/>

<!-- <link rel="stylesheet" type="text/css" href="style.css"> -->

<meta name="viewport" content="width=device-width, initial-scale=1">
<!--

-->
<link rel="stylesheet" href="style.css" type="text/css">
<script src="js/graphic.js">
</script>
<script src="js/player.js">
</script>
<script src="js/game.js">
</script>
<body>

<script>
    let a = new Graphic();
    console.log(a)
    a.drawmainframe();
    a.drawboards([1,2,3,4]);
</script>

<?php
require 'php/computeronly/game.php';

function playcomputer() {
    $game = new Game();
    $game->addplayer("bea");
    $game->addplayer("frank");
    $game->addplayer("hugo");
    $game->startgame();
}

?>


</body>
</html>
