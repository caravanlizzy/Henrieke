<?php

class Player{
    public $name;
    public $cards;
    public $crowns;
    public $strategy;

    function __construct($name) {
        $this->name = $name;
        $this->cards = range(0, 10);
        $this->crowns = 0;
        $this->strategy = "random";
    }

    function playcard() {
        // print_r($this->cards);
        if ($this->strategy == "random") {
            $card = array_rand($this->cards);
        } 
        return $card;
    }

    function removehighestcards($amount = 1) {
        for($i = 0; $i < $amount; $i++) {
            if (array_slice($this->cards, -1, 1, true) != 0) {
                // print_r($this->cards);
                array_pop($this->cards);
            }
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