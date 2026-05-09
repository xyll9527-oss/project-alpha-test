/**
 * 标签接口定义
 */
export interface Tag {
  id: number;
  name: string;
  color: string;
}

/**
 * 工单接口定义
 */
export interface Ticket {
  id: number;
  name: string;
  description?: string;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

/**
 * 分页响应接口定义
 */
export interface PageResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 创建工单请求接口
 */
export interface TicketCreate {
  name: string;
  description?: string;
  status?: string;
  tag_ids?: number[];
}

/**
 * 更新工单请求接口
 */
export interface TicketUpdate {
  name?: string;
  description?: string;
  status?: string;
}

/**
 * 创建标签请求接口
 */
export interface TagCreate {
  name: string;
  color?: string;
}

/**
 * 工单查询参数
 */
export interface TicketQueryParams {
  search?: string;
  tag_id?: number;
  page?: number;
  page_size?: number;
}
