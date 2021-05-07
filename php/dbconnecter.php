<?php
class DbConnecter{
  // create player, game, move
    function __construct($conn, $gameId = 0) {
        $this->conn = $conn;
        $this->gameId = $gameId;
    }

    // create a game
    function getHighestGameId() {
        $sql = "SELECT MAX(gameId) FROM Games";
        $result = $this->conn->query($sql);
        $gameId = $result->fetch_assoc()['MAX(gameId)'];
        return $gameId;
    }

    function createGame($gameId) {
        $sql = "INSERT INTO Games (gameId, playerCount, round, state) VALUES ('$gameId', '0', '0', 'idle')";
        $this->conn->query($sql);
        return $gameId;
    }

    function isUnique($pw) {
        $sql = "SELECT COUNT(*) FROM Players WHERE pw ='$pw'";
        $result = $this->conn->query($sql);
        $result = $result->fetch_assoc()['COUNT(*)'];
        if($result == 0) {
            return TRUE;
        }   else{
            return FALSE;
        }
    }

    function getPw($playerId) {
        $sql = "SELECT pw FROM Players WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $result = $this->conn->query($sql);
        $pw = $result->fetch_assoc()['pw'];
        return $pw;
    }

    function deleteGame() {
        $sql = "DELETE FROM Games WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
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

    function getRound() {
        $sql = "SELECT round FROM Games WHERE gameId='$this->gameId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['round'];
    }

    function setRound($round) {
        $sql = "UPDATE Games SET round='$round' WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }
    function increaseRound() {
        $curRound = $this->getRound();
        $newRound = $curRound + 1;
        $this->setRound($newRound);
    }

    function createPlayer($nick, $pw, $computer = 0){
        $playerId = $this->getPlayerCount() + 1; //playerId might need an improvement for proper player removing
        $sql = "INSERT INTO Players (gameId, playerId, nick, crowns, cards, computer, pw) VALUES ('$this->gameId', '$playerId', '$nick', '0', '11111111111', '$computer', '$pw')";
        $this->conn->query($sql);
        return $playerId;
    }

    function deletePlayer($playerId) {
        $sql = "DELETE FROM Players WHERE playerId='$playerId' AND gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function deleteAllPlayers() {
        $sql = "DELETE FROM Players WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function getPlayerCount() {
        $sql = "SELECT playerCount FROM Games WHERE gameId='$this->gameId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['playerCount'];
    }

    function increasePlayerCount() {
        $newPlayerCount = $this->getPlayerCount() + 1;
        $sql = "UPDATE Games SET playerCount='$newPlayerCount' WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function getPlayerIds() {
        $playerIds = array();
        $sql = "SELECT playerId From Players WHERE gameId='$this->gameId' ORDER BY playerId ASC";
        $result = $this->conn->query($sql);
        while($playerId = $result->fetch_row()) {
            array_push($playerIds, $playerId[0]);
        }
        return $playerIds;
    }

    function getCrowns($playerId) {
        $sql = "SELECT crowns FROM Players WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $result = $this->conn->query($sql); 
        return $result->fetch_assoc()['crowns'];
    }

    function addCrown($playerId) {
        $newCrowns = $this->getCrowns($playerId) + 1;
        $sql = "UPDATE Players SET crowns='$newCrowns' WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $this->conn->query($sql);
        return $newCrowns;
    }

    function createMove($playerId) {
        $sql = "INSERT INTO Move (gameId, playerid) VALUES ('$this->gameId', '$playerId')";
        $this->conn->query($sql);
    }

    function deleteMove() {
        $sql = "DELETE FROM Move WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function resetMove() {
        $sql = "UPDATE Move SET card='11' WHERE gameId='$this->gameId'";
        $this->conn->query($sql);
    }

    function setCard($playerId, $card) {
        $sql = "UPDATE Move SET card='$card' WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $this->conn->query($sql);
    }

    function unsetCard($playerId) {
        $sql = "UPDATE Move SET card='11' WHERE gameId='$this->gameId' AND playerId='$playerId";
        $this->conn->query($sql);
    }

    function getCard($playerId) {
        $sql = "SELECT card FROM Move WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['card'];
    }

    function getDeck($playerId) {
        $sql = "SELECT cards from Players WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $result = $this->conn->query($sql);
        return $result->fetch_assoc()['cards'];
    }

    function updateDeck($playerId, $newDeck) {
        $sql = "UPDATE Players SET cards='$newDeck' WHERE gameId='$this->gameId' AND playerId='$playerId'";
        $this->conn->query($sql);
    }

    function checkMoveComplete() {
        $playerIds = $this->getPlayerIds();
        $n = count($playerIds);
        for($i = 0; $i < $n; $i++) {
            $playerId = $playerIds[$i];
            $card = $this->getCard($playerId);
            if($card == 11) {
                return 0;
            }
        }
        return 1;
    }



}
?>