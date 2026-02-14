export interface CallRecord {
  id: string;
  version: number;
  type: string;
  modalities: string[];
  lastModifiedDateTime: string;
  startDateTime: string;
  endDateTime: string;
  joinWebUrl?: string;
  organizer?: Participant;
  participants?: Participant[];
}

export interface Participant {
  id?: string;
  displayName?: string;
  userPrincipalName?: string;
}

export interface CallRecordsResponse {
  callRecords: CallRecord[];
  nextLink: string | null;
}
