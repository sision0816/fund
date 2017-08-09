
<?php
$dbhost = 'localhost';  // mysql服务器主机地址
$dbuser = 'root';            // mysql用户名
$dbpass = 'wangxing';          // mysql用户名密码
$conn = mysqli_connect($dbhost, $dbuser, $dbpass);
if(! $conn )
{
    die('连接失败: ' . mysqli_error($conn));
}
// 设置编码，防止中文乱码
mysqli_query($conn , "set names utf8");
 
$sql = 'SELECT * FROM fund_info';
 
mysqli_select_db( $conn, 'fund' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('无法读取数据: ' . mysqli_error($conn));
}
echo '<h2> mysqli_fetch_array 测试<h2>';
echo '<table border="1"><tr><td>基金代码 ID</td><td>基金全称</td><td>基金管理人</td><td>发行日期</td></tr>';
while($row = mysqli_fetch_array($retval, MYSQL_ASSOC))
{
    echo "<tr><td> {$row['fund_code']}</td> ".
         "<td>{$row['fund_name']} </td> ".
         "<td>{$row['fund_manager']} </td> ".
         "<td>{$row['issue_date']} </td> ".
         "</tr>";
}
echo '</table>';
mysqli_close($conn);
?>
