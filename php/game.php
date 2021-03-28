<?php

class Player{
    public $name;
    public $cards;
    public $crowns;
    public $strategy;

    function __contruct($name) {
        $this->name = $name;
        $this->cards = range(0, 10);
        $this->crowns = 0;
        $this->strategy = "random";
    }

    function playcard() {
        if ($this->strategy == "random") {
            $card = array_rand($this->cards);
        }
    }

    function removehighestcard() {
        if ($this->cards[-1] != 0) {
            array_pop($this->cards);
        }
    }

    function removecard($card) {
        $index = array_search($card, $this->cards);
        if ($index != 0) {
            array_splice($this->cards, $index);
        }
    }

    function addcrown() {
        $this->crowns += 1;
    }

    function changename($newname) {
        $this->name = $newname;
    }

    function reset() {
        $this->cards = range(0, 10);
        $this->crowns = 0;
    }
}



?>