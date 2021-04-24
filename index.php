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
<body>


<?php

require 'php/game.php';

$game = new Game();
$game->addplayer("bea");
$game->addplayer("frank");
$game->addplayer("hugo");
$game->startgame();

?>
<script>
    let a = new Graphic();
    a.drawmainframe();
</script>

</body>
</html>
