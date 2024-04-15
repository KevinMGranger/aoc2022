open Aoc2022

let day = ref ""
let part = ref ""
let filename = ref ""

let anon arg =
  if !day = "" then day := arg
  else if !part = "" then part := arg
  else if !filename = "" then filename := arg
  else invalid_arg "too many args"

let () =
  Arg.parse [] anon "aoc2022 DAYPART FILENAME";
  if (!day = "" || !part = "" || !filename = "") then invalid_arg "not enough args"
  else ()

(* let () =
  print_endline !day;
  print_endline !filename *)

let parseDay day =
  match day with
  | "1" -> Day1.part1, Day1.part2
  | "2" -> Day2.part1, Day2.part2
  | "3" -> Day3.part1, Day3.part2
  | _ -> invalid_arg "no day with that number"

let handlePart part (p1, p2) = match part with
  | "1" -> p1
  | "2" -> p2
  | _ -> invalid_arg "unknown part"

let () = (parseDay !day |> handlePart !part) @@ !filename

(* let () = Array.get Sys.argv 1 |> fun file -> In_channel.with_open_text file parse_calories |> sum_all |> print_int *)