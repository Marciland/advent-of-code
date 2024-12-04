extern crate regex;

mod word_search;

use word_search::WordSearch;

pub fn star1(input: &[String]) {
    /*
       Find xmas:
           horizontally
           vertically
           diagonally
           for and backwards
    */
    let word_search = WordSearch::from(input);

    let total = word_search.find("XMAS");

    println!("{total}");
}

pub fn star2(input: &[String]) {
    /*
        search for MAS in an X form where A is in the middle
        eg.
            M.S
            .A.
            M.S

        how many X-Mas?
    */
    let word_search = WordSearch::from(input);

    let total = word_search.search_x_mas();

    println!("{total}");
}
