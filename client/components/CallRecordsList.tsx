import React from 'react';
import type { CallRecord } from '../types/callRecord';

interface CallRecordsListProps {
  records: CallRecord[];
}

export const CallRecordsList: React.FC<CallRecordsListProps> = ({ records }) => {
  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const calculateDuration = (start: string, end: string) => {
    const startTime = new Date(start).getTime();
    const endTime = new Date(end).getTime();
    const durationMs = endTime - startTime;
    const minutes = Math.floor(durationMs / 60000);
    const seconds = Math.floor((durationMs % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  return (
    <div className="call-records-list">
      <h2>Call Records ({records.length})</h2>
      <div className="records-table-container">
        <table className="records-table">
          <thead>
            <tr>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Duration</th>
              <th>Type</th>
              <th>Modalities</th>
              <th>ID</th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr key={record.id}>
                <td>{formatDateTime(record.startDateTime)}</td>
                <td>{formatDateTime(record.endDateTime)}</td>
                <td>{calculateDuration(record.startDateTime, record.endDateTime)}</td>
                <td>{record.type}</td>
                <td>{record.modalities?.join(', ') || 'N/A'}</td>
                <td className="record-id">{record.id.substring(0, 20)}...</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
