import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(
  id: string,
  name: string,
  numberOfDevice: number,
  remark?: string
) {
  return { id, name, numberOfDevice, remark };
}

const rows = [
  createData("001", "书画保存监测2022-02-01", 1),
];

export default function ProjectTable() {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>工程ID</TableCell>
            <TableCell align="right">名称</TableCell>
            <TableCell align="right">监测装置数量</TableCell>
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
              <TableCell align="right">{row.name}</TableCell>
              <TableCell align="right">{row.numberOfDevice}</TableCell>
              <TableCell align="right">{row.remark}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
