<template>
  <div class="ticket-list">
    <div
      v-for="ticket in tickets"
      :key="ticket.id"
      class="ticket-card"
      :class="{ completed: ticket.status === 'completed' }"
    >
      <!-- 左侧：状态指示器 -->
      <div class="ticket-status-indicator" @click="toggleStatus(ticket)">
        <div class="status-checkbox" :class="ticket.status">
          <svg v-if="ticket.status === 'completed'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M5 13l4 4L19 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>

      <!-- 中间：内容区 -->
      <div class="ticket-content" @click="editTicket(ticket)">
        <div class="ticket-header">
          <h3 class="ticket-title">{{ ticket.name }}</h3>
          <span class="ticket-date">{{ formatDate(ticket.created_at) }}</span>
        </div>
        
        <p v-if="ticket.description" class="ticket-desc">
          {{ ticket.description }}
        </p>

        <!-- 标签列表 -->
        <div v-if="ticket.tags.length > 0" class="ticket-tags">
          <span
            v-for="tag in ticket.tags"
            :key="tag.id"
            class="tag-badge"
            :style="{ 
              backgroundColor: tag.color + '20',
              color: tag.color,
              borderColor: tag.color + '40'
            }"
          >
            {{ tag.name }}
          </span>
        </div>
      </div>

      <!-- 右侧：操作区 -->
      <div class="ticket-actions">
        <button class="action-btn edit" @click="editTicket(ticket)" title="编辑">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke-width="2" stroke-linecap="round"/>
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
        <button class="action-btn delete" @click="deleteTicket(ticket.id)" title="删除">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Ticket } from '@/types';

const props = defineProps<{
  tickets: Ticket[];
}>();

const emit = defineEmits<{
  (e: 'edit', ticket: Ticket): void;
  (e: 'delete', id: number): void;
  (e: 'toggle-status', id: number, status: string): void;
}>();

/**
 * 格式化日期
 */
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  
  // 小于1小时
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000);
    return minutes < 1 ? '刚刚' : `${minutes} 分钟前`;
  }
  
  // 小于24小时
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours} 小时前`;
  }
  
  // 小于7天
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000);
    return `${days} 天前`;
  }
  
  // 默认显示日期
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  });
};

/**
 * 编辑工单
 */
const editTicket = (ticket: Ticket) => {
  emit('edit', ticket);
};

/**
 * 删除工单
 */
const deleteTicket = (id: number) => {
  emit('delete', id);
};

/**
 * 切换工单状态
 */
const toggleStatus = (ticket: Ticket) => {
  emit('toggle-status', ticket.id, ticket.status);
};
</script>

<style scoped>
.ticket-list {
  display: flex;
  flex-direction: column;
}

.ticket-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-divider);
  transition: background-color 0.2s;
}

.ticket-card:last-child {
  border-bottom: none;
}

.ticket-card:hover {
  background-color: var(--color-canvas-parchment);
}

.ticket-card.completed {
  opacity: 0.7;
}

.ticket-card.completed .ticket-title {
  text-decoration: line-through;
  color: var(--color-body-muted);
}

/* 状态指示器 */
.ticket-status-indicator {
  flex-shrink: 0;
  padding-top: 2px;
}

.status-checkbox {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid var(--color-hairline);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.status-checkbox:hover {
  border-color: var(--color-primary);
}

.status-checkbox.pending {
  border-color: #ff9500;
  background: transparent;
}

.status-checkbox.completed {
  border-color: #34c759;
  background: #34c759;
}

.status-checkbox svg {
  width: 14px;
  height: 14px;
  color: white;
}

/* 内容区 */
.ticket-content {
  flex: 1;
  min-width: 0;
  cursor: pointer;
}

.ticket-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.ticket-title {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 600;
  color: var(--color-ink);
  line-height: 1.3;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ticket-date {
  font-size: 13px;
  color: var(--color-body-muted);
  flex-shrink: 0;
}

.ticket-desc {
  font-size: 14px;
  color: var(--color-body-muted);
  line-height: 1.5;
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 标签 */
.ticket-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 9999px;
  border: 1px solid;
}

/* 操作按钮 */
.ticket-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.ticket-card:hover .ticket-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
  color: var(--color-body-muted);
}

.action-btn:hover {
  background: var(--color-canvas);
}

.action-btn.edit:hover svg {
  color: var(--color-primary);
}

.action-btn.delete:hover svg {
  color: #ff3b30;
}

/* 响应式 */
@media (max-width: 768px) {
  .ticket-card {
    padding: 16px;
    gap: 12px;
  }

  .ticket-actions {
    opacity: 1;
    flex-direction: column;
  }

  .ticket-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .ticket-title {
    white-space: normal;
  }
}
</style>
