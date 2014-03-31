<?
header('Access-Control-Allow-Origin: *'); 
$conn = mysql_connect("localhost" , "root" , "admin") or die(mysql_error());

$result = mysql_query("SELECT lattitude , langitude , sent_pos , sent_neg FROM happiness_index.geo_tweets" , $conn);
$to_encode = array();
while($row = mysql_fetch_assoc($result)){
	$to_encode[] = $row;
}
echo json_encode($to_encode);
?>
