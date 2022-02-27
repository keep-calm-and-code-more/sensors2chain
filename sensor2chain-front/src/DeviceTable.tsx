import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(
  id: string,
  numberOfSensor: number,
  sensors: string,
  projectID?: string,
  remark?: string
) {
  return { id, numberOfSensor, sensors, projectID, remark };
}

const rows = [
  createData("001d01", 3,"[1,1,1]", "001"),
];

export default function DeviceTable() {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>装置ID</TableCell>
            <TableCell align="right">传感器数量</TableCell>
            <TableCell align="right">包含传感器</TableCell>
            <TableCell align="right">属于项目</TableCell>
            <TableCell align="right">备注</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.id}
              </TableCell>
              <TableCell align="right">{row.numberOfSensor}</TableCell>
              <TableCell align="right">{row.sensors}</TableCell>
              <TableCell align="right">{row.projectID}</TableCell>
              <TableCell align="right">{row.remark}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
