import * as React from 'react';
import { DataGrid, GridToolbar, GridActionsCellItem } from '@mui/x-data-grid';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Chip from '@mui/material/Chip';
import EmptyRowsOverlay from '../../layout/table/EmptyRowsOverlay';
import RefreshIcon from '@mui/icons-material/Cached';
import PendingIcon from '@mui/icons-material/PauseCircleOutline';
import FailedIcon from '@mui/icons-material/ErrorOutline';
import CancelledIcon from '@mui/icons-material/Close';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

import { LightTooltip } from '../../components/tooltip';
import { useNavigate } from 'react-router-dom';
import { formatDate, renderRowIds } from '../../utils/helper';
import stationData from './data/rows.json';

const chipColor = {
  running: { color: 'info', icon: <RefreshIcon /> },
  pending: { color: 'warning', icon: <PendingIcon /> },
  failed: { color: 'error', icon: <FailedIcon /> },
  cancelled: { color: 'primary', icon: <CancelledIcon /> },
};

function Jobs() {
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
      {
        field: 'id',
        headerName: 'Job ID',
        editable: true,
        resizable: false,
        width: 200,
      },
      {
        field: 'state',
        headerName: 'State',
        resizable: false,
        width: 150,
        cellClassName: 'job-summary-state',
        renderCell: (params) => {
          const label = params.value;
          return (
            <Chip
              className="font-semibold"
              variant="outlined"
              size="small"
              sx={{ width: 100 }}
              label={label}
              icon={chipColor[label].icon}
              color={chipColor[label].color}
            />
          );
        },
      },
      { field: 'train', headerName: 'Train Name', width: 150 },
      {
        field: 'currentStation',
        headerName: 'Curr. Station',
        description: 'The current station where the train is executing.',
        resizable: false,
        width: 130,
      },
      { field: 'creator', headerName: 'Creator', resizable: false, width: 120 },
      {
        field: 'description',
        headerName: 'Description',
        resizable: false,
        width: 300,
      },
      {
        field: 'created',
        headerName: 'Created At',
        resizable: false,
        width: 150,
        valueGetter: formatDate,
      },
      {
        field: 'updated',
        headerName: 'Updated At',
        resizable: false,
        width: 150,
        valueGetter: formatDate,
      },
      {
        field: 'actions',
        type: 'actions',
        width: 100,
        resizable: false,
        getActions: (params) => [
          /* eslint-disable react/jsx-key */
          <GridActionsCellItem
            icon={
              <LightTooltip
                disableInteractive
                placement="left"
                title="View details"
              >
                <OpenInNewIcon />
              </LightTooltip>
            }
            onClick={() => navigate('44bc00a0-9208-11ef-a539-579e5c650fb5')}
            label="Delete"
          />,
        ],
      },
    ],
    []
  );

  return (
    <>
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Jobs
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
      {/* <Grid container spacing={2}>
        <Grid size={{ md: 4, sm: 6, xs: 12 }}>
          <SummaryCard type="cpu" title="CPU Usage" value={35} percent />
        </Grid>
        <Grid size={{ md: 4, sm: 6, xs: 12 }}>
          <SummaryCard type="memory" title="Memory Usage" value={12} percent />
        </Grid>
        <Grid size={{ md: 4, sm: 12, xs: 12 }}>
          <SummaryCard
            type="network"
            title="Network Usage"
            value={10}
            percent
          />
        </Grid>
        <Grid size={{ xs: 12 }}>
          <Paper
            elevation={0}
            className="flex h-[calc(100dvh-310px)] min-h-96"
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
              columns={jobCols}
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
        </Grid>
      </Grid> */}
    </>
  );
}

export default Jobs;
