
(* merely for testing. *)
(* let read_first file = 
  let read_and_print ic = In_channel.input_line ic |> Option.map print_endline |> ignore in
  In_channel.with_open_text file read_and_print *)

  let parse_single_elf (inch: in_channel) : int list * bool =
    let rec parsely list_so_far = match In_channel.input_line inch with
      | Some "" -> list_so_far, false
      | Some str -> parsely (list_so_far @ [int_of_string str])
      | None -> list_so_far, true
    in
    parsely []
  
  let parse_calories (inch: in_channel) : int list list =
    let rec parsely elves_so_far = match parse_single_elf inch with
      | list, true -> elves_so_far @ [list]
      | list, false -> parsely (elves_so_far @ [list])
    in
    parsely []
  
  let elf_sum = List.map (List.fold_left (+) 0)
  
  let sum_all (elves : int list list) = elf_sum elves |> List.fold_left max 0
  
  let checkMax ((one, two, three) as top) newInt =
    if newInt >= one then newInt, one, two
    else if newInt >= two then one, newInt, two
    else if newInt >= three then one, two, newInt
    else top
  
  let printMax (one, two, three) = Printf.printf "%d\n%d\n%d\n" one two three
  
  
let part1 file = In_channel.with_open_text file parse_calories |> sum_all |> print_int

let part2 file = In_channel.with_open_text file parse_calories |> elf_sum |> List.fold_left checkMax (0, 0, 0) |> fun ((one, two, three) as top) ->
  printMax top;
  print_int (one + two + three)