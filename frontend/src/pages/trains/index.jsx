import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { DataGrid, GridActionsCellItem, GridToolbar } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

import { LightTooltip } from '../../components/tooltip';
import { formatDate, renderRowIds } from '../../utils/helper';
import EmptyRowsOverlay from '../../layout/table/EmptyRowsOverlay';
import trainData from './data/rows.json';

export default function Trains() {
  const navigate = useNavigate();

  const columns = React.useMemo(
    () => [
      {
        field: 'lineNo',
        headerName: '#',
        width: 60,
        editable: false,
        resizable: false,
        sortable: false,
        disableColumnMenu: true,
        renderCell: renderRowIds,
      },
      { field: 'id', headerName: 'Train ID', width: 180, editable: true },
      { field: 'name', headerName: 'Title', width: 190, editable: true },
      { field: 'creator', headerName: 'Creator', width: 130 },
      { field: 'description', headerName: 'Description', width: 320 },
      {
        field: 'created',
        headerName: 'Created at',
        width: 150,
        valueGetter: formatDate,
      },
      {
        field: 'updated',
        headerName: 'Updated at',
        width: 150,
        valueGetter: formatDate,
      },
      { field: 'version', headerName: 'Version', width: 80 },
      {
        field: 'actions',
        type: 'actions',
        getActions: (params) => [
          /* eslint-disable react/jsx-key */
          <GridActionsCellItem
            label="View train details"
            icon={
              <LightTooltip
                disableInteractive
                placement="left"
                title="View details"
              >
                <OpenInNewIcon />
              </LightTooltip>
            }
            onClick={() => navigate('hello-world')}
          />,
          <GridActionsCellItem
            icon={<FileCopyIcon />}
            onClick={() => console.log(params)}
            label="Print"
            showInMenu
          />,
        ],
      },
    ],
    [navigate]
  );

  return (
    <>
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Trains
      </Typography>
      <Paper
        elevation={0}
        className="flex h-[calc(100dvh-210px)] min-h-96"
        sx={{
          '& .MuiDataGrid-toolbarContainer': {
            paddingTop: 0.6,
            paddingBottom: 0.5,
            paddingLeft: 0.8,
          },
          '& .MuiDataGrid-columnHeaderTitle': {
            fontWeight: 600,
          },
        }}
      >
        <DataGrid
          rows={trainData}
          columns={columns}
          pageSizeOptions={[20]}
          disableRowSelectionOnClick
          initialState={{
            density: 'comfortable',
            pagination: {
              paginationModel: {
                pageSize: 20,
              },
            },
          }}
          slots={{ noRowsOverlay: EmptyRowsOverlay, toolbar: GridToolbar }}
          slotProps={{
            toolbar: {
              showQuickFilter: true,
            },
          }}
        />
      </Paper>
    </>
  );
}
