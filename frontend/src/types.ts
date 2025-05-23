export interface Query {
    text: string;
}

export interface QueryResponse {
    query: string;
    answer: string;
    timestamp?: string;
}

export interface Document {
    content: string;
} 