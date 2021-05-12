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
    game.setupGraphic();

</script>

<?php
require 'php/computeronly/game.php';
?>


</body>
</html>
