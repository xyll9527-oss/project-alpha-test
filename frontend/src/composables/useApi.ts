import { ref } from 'vue';
import axios from 'axios';
import type { Ticket, Tag, PageResponse, TicketCreate, TicketUpdate, TagCreate, TicketQueryParams } from '@/types';

/**
 * API基础地址
 */
const API_BASE = 'http://localhost:8000/api';

/**
 * 创建axios实例
 */
const axiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * API调用组合式函数
 */
export function useApi() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  /**
   * 获取工单列表
   * @param params 查询参数
   * @returns 分页响应数据
   */
  const getTickets = async (params?: TicketQueryParams): Promise<PageResponse<Ticket>> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.get<PageResponse<Ticket>>('/tickets', { params });
      return response.data;
    } catch (e) {
      error.value = '获取工单列表失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 获取单个工单
   * @param id 工单ID
   * @returns 工单详情
   */
  const getTicket = async (id: number): Promise<Ticket> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.get<Ticket>(`/tickets/${id}`);
      return response.data;
    } catch (e) {
      error.value = '获取工单详情失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 创建工单
   * @param data 工单数据
   * @returns 创建的工单
   */
  const createTicket = async (data: TicketCreate): Promise<Ticket> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.post<Ticket>('/tickets', data);
      return response.data;
    } catch (e) {
      error.value = '创建工单失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 更新工单
   * @param id 工单ID
   * @param data 更新数据
   * @returns 更新后的工单
   */
  const updateTicket = async (id: number, data: TicketUpdate): Promise<Ticket> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.put<Ticket>(`/tickets/${id}`, data);
      return response.data;
    } catch (e) {
      error.value = '更新工单失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 删除工单
   * @param id 工单ID
   */
  const deleteTicket = async (id: number): Promise<void> => {
    loading.value = true;
    error.value = null;
    try {
      await axiosInstance.delete(`/tickets/${id}`);
    } catch (e) {
      error.value = '删除工单失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 更新工单状态
   * @param id 工单ID
   * @param status 新状态
   * @returns 更新后的工单
   */
  const updateTicketStatus = async (id: number, status: string): Promise<Ticket> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.patch<Ticket>(`/tickets/${id}/status`, { status });
      return response.data;
    } catch (e) {
      error.value = '更新工单状态失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 为工单添加标签
   * @param ticketId 工单ID
   * @param tagId 标签ID
   * @returns 更新后的工单
   */
  const addTagToTicket = async (ticketId: number, tagId: number): Promise<Ticket> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.post<Ticket>(`/tickets/${ticketId}/tags/${tagId}`);
      return response.data;
    } catch (e) {
      error.value = '添加标签失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 从工单移除标签
   * @param ticketId 工单ID
   * @param tagId 标签ID
   * @returns 更新后的工单
   */
  const removeTagFromTicket = async (ticketId: number, tagId: number): Promise<Ticket> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.delete<Ticket>(`/tickets/${ticketId}/tags/${tagId}`);
      return response.data;
    } catch (e) {
      error.value = '移除标签失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 获取所有标签
   * @returns 标签列表
   */
  const getTags = async (): Promise<Tag[]> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.get<Tag[]>('/tags');
      return response.data;
    } catch (e) {
      error.value = '获取标签列表失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 创建标签
   * @param data 标签数据
   * @returns 创建的标签
   */
  const createTag = async (data: TagCreate): Promise<Tag> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.post<Tag>('/tags', data);
      return response.data;
    } catch (e) {
      error.value = '创建标签失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 删除标签
   * @param id 标签ID
   */
  const deleteTag = async (id: number): Promise<void> => {
    loading.value = true;
    error.value = null;
    try {
      await axiosInstance.delete(`/tags/${id}`);
    } catch (e) {
      error.value = '删除标签失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 获取工单统计
   * @returns 统计信息
   */
  const getTicketsStats = async (): Promise<{ total: number; pending: number; completed: number }> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axiosInstance.get('/tickets/stats/count');
      return response.data;
    } catch (e) {
      error.value = '获取工单统计失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    getTickets,
    getTicket,
    createTicket,
    updateTicket,
    deleteTicket,
    updateTicketStatus,
    addTagToTicket,
    removeTagFromTicket,
    getTags,
    createTag,
    deleteTag,
    getTicketsStats
  };
}
