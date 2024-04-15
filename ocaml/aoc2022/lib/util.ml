exception Unimplemented of string

let unimplemented msg = raise @@ Unimplemented msg

let list_tap f l =
  List.map (fun x -> f x; x) l

let tuple_map f (first, second) = (f first), (f second)

let list_sum = List.fold_left (+) 0