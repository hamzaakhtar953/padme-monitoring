import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { DataGrid, GridToolbar, GridActionsCellItem } from '@mui/x-data-grid';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import EmptyRowsOverlay from '../../layout/table/EmptyRowsOverlay';
import stationData from './data/rows.json';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import { LightTooltip } from '../../components/tooltip';
import { formatDate, renderRowIds } from '../../utils/helper';

export default function Stations() {
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
      { field: 'id', headerName: 'Station ID', width: 200, editable: true },
      { field: 'name', headerName: 'Name', width: 150 },
      { field: 'owner', headerName: 'Owner', width: 150 },
      { field: 'description', headerName: 'Description', width: 300 },
      { field: 'longitude', headerName: 'Longitude', width: 120 },
      { field: 'latitude', headerName: 'Latitute', width: 120 },
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
      {
        field: 'actions',
        type: 'actions',
        pinned: 'right', // Pin the last column to the right
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
            onClick={() => navigate('Klee')}
          />,
        ],
      },
    ],
    [navigate]
  );

  return (
    <>
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Stations
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
          rows={stationData}
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
