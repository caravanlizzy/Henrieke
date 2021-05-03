<?php
class Game{
  // create player, game, move
    function __construct($conn, $gameId) {
        $this->conn = $conn;
        $this->gameId = $gameId;
    }

    // create a game
    function createGame() {
        $sql = "INSERT INTO Games (gameId, playerCount, round, state) VALUES ('$this->gameId', '0', '0', 'idle')";
        $this->conn->query($sql);
    }

    function createPlayer($nick){
        $playerId = $this->getPlayerCount() + 1;
        $sql = "INSERT INTO Players (gameId, playerId, nick, crowns, cards, computer) VALUES ('$this->gameId', '$playerId', '$nick', '0', '11111111111', '0')";
        $this->conn->query($sql);
        return $playerId;
    }


    //access table column
    function getPlayerCount() {
        $sql = "SELECT playerCount FROM Games WHERE gameId='$this->gameId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['playerCount'];
    }

    function setGameState($newState) {
        $sql = "UPDATE Games SET state='$newState' WHERE gameId='$this->gameId'";
        $this->conn->query($sql); 
    }

    function getGameState() {
        $sql = "SELECT state FROM Games WHERE gameId='$this->gameId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['state'];
    }

    function increasePlayerCount() {
        $newPlayerCount = $this->getPlayerCount() + 1;
        $sql = "UPDATE Games SET playerCount='$newPlayerCount' WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function increaseRound() {
        $curRound = $this->getRound();
        $newRound = $curRound + 1;
        $sql = "UPDATE Games SET round='$newRound' WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function getRound() {
        $sql = "SELECT round FROM Games WHERE gameId='$this->gameId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['round'];
    }

    //create
    function createMove($playerId) {
        $sql = "INSERT INTO Move (gameId, playerid) VALUES ('$this->gameId', '$playerId')";
        $this->conn->query($sql);
    }

    function setCard($playerId, $card) {
        $sql = "UPDATE Moves SET card='$card' WHERE gameId='$this->gameId' AND playerId='$playerId";
        $this->conn->query($sql);
    }

    function unsetCard($playerId) {
        $sql = "UPDATE Moves SET card='NULL' WHERE gameId='$this->gameId' AND playerId='$playerId";
        $this->conn->query($sql);
    }

    function addPlayer($nick) {
        $playerId = $this->createPlayer($nick);
        $this->increasePlayerCount();
        $this->createMove($playerId);
    }

    // function setupPlayers($playerList) {
    //     foreach($playerList as $player) {

    //     }
    // }

    // function setupGame($playerList) {
    //     $this->createGame();
    //     // $this->setupPlayers($playerList);
    // }
  
}
?>