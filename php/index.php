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
<body>


<?php

require 'game.php';

$game = new Game();
$game->addplayer("bea");
$game->addplayer("frank");
$game->addplayer("hugo");
$game->startgame();

?>


</body>
</html>
