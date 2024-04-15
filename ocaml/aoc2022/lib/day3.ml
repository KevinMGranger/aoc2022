open Util

type rucksack = string * string

let rucksack_of_line line : rucksack =
  let len = String.length line in
  (String.sub line 0 (len/2)), (String.sub line (len/2) (len/2))

module CharSet = Set.Make(Char)


type setsack = CharSet.t * CharSet.t

let charset_of_string = String.fold_left (fun acc char -> CharSet.add char acc) CharSet.empty

let setsack_of_rucksack ((first, second) : rucksack) : setsack = charset_of_string first, charset_of_string second

let shared_in_setsack ((first, second) : setsack) = CharSet.inter first second

let value_of_char char =
  if Char.lowercase_ascii char = char then (Char.code char) - 96
  else ((Char.code char) - 64) + 26

let shared_value setsack = shared_in_setsack setsack |> CharSet.elements |> List.map value_of_char |> List.fold_left (+) 0

let elf_groups = 

let part1 file = In_channel.with_open_text file In_channel.input_lines |> List.map (fun x -> rucksack_of_line x |> setsack_of_rucksack |> shared_value) |> list_sum |> print_int
let part2 file = ignore file; Util.unimplemented "part2"