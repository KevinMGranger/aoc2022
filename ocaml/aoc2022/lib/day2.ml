type shape =
  | Rock
  | Paper
  | Scissors
  [@@deriving Sexp]

let string_of_shape shape = match shape with
  | Rock -> "Rock"
  | Paper -> "Paper"
  | Scissors -> "Scissors"

let shape_of_char char = match char with 
  | 'A' | 'X' -> Rock
  | 'B' | 'Y' -> Paper
  | 'C' | 'Z' -> Scissors
  | _ -> invalid_arg "bad char"

let score_of_shape shape = match shape with
  | Rock -> 1
  | Paper -> 2
  | Scissors -> 3

type outcome =
  | Loss
  | Draw
  | Win

let outcome_of_char char = match char with 
  | 'X' -> Loss
  | 'Y' -> Draw
  | 'Z' -> Win
  | _ -> invalid_arg "bad outcome char"

let score_of_outcome outcome = match outcome with
  | Loss -> 0
  | Draw -> 3
  | Win -> 6

let score_for_round opponent_shape your_shape = 
  let outcome = match opponent_shape, your_shape with
  | Rock, Rock | Paper, Paper | Scissors, Scissors -> Draw 
  | Rock, Paper | Paper, Scissors | Scissors, Rock -> Win
  | Paper, Rock | Scissors, Paper | Rock, Scissors -> Loss
in
  score_of_outcome outcome + score_of_shape your_shape

let shape_for_outcome opponent_shape outcome = match opponent_shape, outcome with
  | Rock, Draw | Scissors, Win | Paper, Loss -> Rock
  | Paper, Draw | Rock, Win | Scissors, Loss -> Paper
  | Scissors, Draw | Paper, Win | Rock, Loss -> Scissors

let parse_shapes (line: string) = (shape_of_char @@ String.get line 0), (shape_of_char @@ String.get line 2)
let parse_shape_outcome (line : string) = (shape_of_char @@ String.get line 0), (outcome_of_char @@ String.get line 2)

  (* let game = "A X
B Y
C Z" in *)
  (* let game = String.split_on_char '\n' game |> List.map parse_match *)

let run_game game =
  List.map (fun (x, y) -> score_for_round x y) game |> List.fold_left (+) 0 
    

let parse_file_as_shapes inch = In_channel.input_lines inch |> List.map parse_shapes
let parse_file_as_shapes_and_outcomes inch = In_channel.input_lines inch |> List.map parse_shape_outcome

let part1 file = In_channel.with_open_text file parse_file_as_shapes |> run_game |> print_int
let part2 file = In_channel.with_open_text file parse_file_as_shapes_and_outcomes |> List.map (fun (shape, outcome) -> (shape, shape_for_outcome shape outcome)) |> run_game |> print_int