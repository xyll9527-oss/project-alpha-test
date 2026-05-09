<template>
  <div class="app">
    <!-- 全局导航栏 -->
    <nav class="global-nav">
      <div class="nav-content">
        <div class="nav-brand">
          <span class="brand-icon">◆</span>
          <span class="brand-text">Project Alpha</span>
        </div>
        <div class="nav-actions">
          <button class="nav-btn" @click="openTagManager">
            管理标签
          </button>
          <button class="nav-btn-primary" @click="openCreateForm">
            <span class="btn-icon">+</span>
            <span>新建 Ticket</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 搜索栏 -->
      <section class="search-section">
        <div class="search-container">
          <div class="search-input-wrapper">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8" stroke-width="2"/>
              <path d="m21 21-4.35-4.35" stroke-width="2"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="search-input"
              placeholder="搜索 Ticket..."
              @keyup.enter="handleSearch"
            />
          </div>
        </div>
      </section>

      <!-- 标签筛选 -->
      <TagFilter
        :tags="tags"
        :selected-tag="selectedTag"
        @select="handleTagSelect"
      />

      <!-- 状态筛选 -->
      <section class="status-section">
        <div class="status-tabs">
          <button
            v-for="tab in statusTabs"
            :key="tab.value"
            class="status-tab"
            :class="{ active: selectedStatus === tab.value }"
            @click="handleStatusSelect(tab.value)"
          >
            <span class="tab-dot" :class="tab.value"></span>
            <span class="tab-label">{{ tab.label }}</span>
            <span v-if="tab.count > 0" class="tab-count">{{ tab.count }}</span>
          </button>
        </div>
      </section>

      <!-- Ticket 列表 -->
      <section class="tickets-section" v-loading="loading">
        <div class="section-header">
          <h2 class="section-title">{{ currentSectionTitle }}</h2>
          <span class="section-count">{{ total }} 个 Ticket</span>
        </div>

        <TicketList
          :tickets="tickets"
          @edit="openEditForm"
          @delete="handleDelete"
          @toggle-status="handleToggleStatus"
        />

        <!-- 分页 -->
        <div v-if="total > 0" class="pagination">
          <div class="pagination-info">
            第 {{ currentPage }} 页，共 {{ Math.ceil(total / pageSize) }} 页
          </div>
          <div class="pagination-controls">
            <button
              class="pagination-btn"
              :disabled="currentPage === 1"
              @click="handlePageChange(currentPage - 1)"
            >
              上一页
            </button>
            <div class="page-numbers">
              <button
                v-for="page in displayedPages"
                :key="page"
                class="page-number"
                :class="{ active: currentPage === page }"
                @click="handlePageChange(page)"
              >
                {{ page }}
              </button>
            </div>
            <button
              class="pagination-btn"
              :disabled="currentPage >= Math.ceil(total / pageSize)"
              @click="handlePageChange(currentPage + 1)"
            >
              下一页
            </button>
          </div>
          <div class="page-size-selector">
            <select v-model="pageSize" @change="handleSizeChange">
              <option :value="10">10 / 页</option>
              <option :value="20">20 / 页</option>
              <option :value="50">50 / 页</option>
            </select>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && tickets.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <h3 class="empty-title">暂无 Ticket</h3>
          <p class="empty-desc">创建一个新的 Ticket 开始管理您的工作</p>
          <button class="empty-btn" @click="openCreateForm">
            创建 Ticket
          </button>
        </div>
      </section>
    </main>

    <!-- 创建/编辑工单弹窗 -->
    <TicketForm
      :visible="showForm"
      :ticket="editingTicket"
      :tags="tags"
      @close="closeForm"
      @submit="handleFormSubmit"
    />

    <!-- 标签管理弹窗 -->
    <TagManager
      :visible="showTagManager"
      :tags="tags"
      @close="closeTagManager"
      @update="refreshTags"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import type { Ticket, Tag } from '@/types';
import { useApi } from '@/composables/useApi';
import TicketList from '@/components/TicketList.vue';
import TicketForm from '@/components/TicketForm.vue';
import TagFilter from '@/components/TagFilter.vue';
import TagManager from '@/components/TagManager.vue';

const api = useApi();

// 数据状态
const tickets = ref<Ticket[]>([]);
const tags = ref<Tag[]>([]);
const loading = ref(false);

// 分页状态
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 查询状态
const searchQuery = ref('');
const selectedTag = ref<number | null>(null);
const selectedStatus = ref<string>('all');

// 弹窗状态
const showForm = ref(false);
const editingTicket = ref<Ticket | null>(null);
const showTagManager = ref(false);

// 工单统计
const ticketStats = ref({ total: 0, pending: 0, completed: 0 });

// 状态标签
const statusTabs = computed(() => [
  { label: '全部', value: 'all', count: ticketStats.value.total },
  { label: '待办', value: 'pending', count: ticketStats.value.pending },
  { label: '已完成', value: 'completed', count: ticketStats.value.completed },
]);

// 当前区块标题
const currentSectionTitle = computed(() => {
  if (selectedStatus.value === 'pending') return '待办事项';
  if (selectedStatus.value === 'completed') return '已完成';
  return '全部 Ticket';
});

// 显示的页码
const displayedPages = computed(() => {
  const totalPages = Math.ceil(total.value / pageSize.value);
  const current = currentPage.value;
  const pages: number[] = [];

  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    if (current <= 3) {
      pages.push(1, 2, 3, 4, 5, -1, totalPages);
    } else if (current >= totalPages - 2) {
      pages.push(1, -1, totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
    } else {
      pages.push(1, -1, current - 1, current, current + 1, -1, totalPages);
    }
  }
  return pages;
});

/**
 * 加载工单列表
 */
const loadTickets = async () => {
  loading.value = true;
  try {
    const response = await api.getTickets({
      search: searchQuery.value || undefined,
      tag_id: selectedTag.value || undefined,
      status: selectedStatus.value === 'all' ? undefined : selectedStatus.value,
      page: currentPage.value,
      page_size: pageSize.value
    });
    tickets.value = response.data;
    total.value = response.total;
  } catch (e) {
    console.error('Failed to load tickets:', e);
  } finally {
    loading.value = false;
  }
};

/**
 * 加载标签列表
 */
const loadTags = async () => {
  try {
    tags.value = await api.getTags();
  } catch (e) {
    console.error('Failed to load tags:', e);
  }
};

/**
 * 加载工单统计
 */
const loadTicketStats = async () => {
  try {
    ticketStats.value = await api.getTicketsStats();
  } catch (e) {
    console.error('Failed to load ticket stats:', e);
  }
};

/**
 * 刷新标签列表
 */
const refreshTags = () => {
  loadTags();
};

/**
 * 搜索处理
 */
const handleSearch = () => {
  currentPage.value = 1;
  loadTickets();
};

/**
 * 标签选择处理
 */
const handleTagSelect = (tagId: number | null) => {
  selectedTag.value = tagId;
  currentPage.value = 1;
  loadTickets();
};

/**
 * 状态选择处理
 */
const handleStatusSelect = (status: string) => {
  selectedStatus.value = status;
  currentPage.value = 1;
  loadTickets();
};

/**
 * 分页大小变更
 */
const handleSizeChange = () => {
  currentPage.value = 1;
  loadTickets();
};

/**
 * 页码变更
 */
const handlePageChange = (page: number) => {
  if (page < 1 || page > Math.ceil(total.value / pageSize.value)) return;
  currentPage.value = page;
  loadTickets();
};

/**
 * 打开创建表单
 */
const openCreateForm = () => {
  editingTicket.value = null;
  showForm.value = true;
};

/**
 * 打开编辑表单
 */
const openEditForm = (ticket: Ticket) => {
  editingTicket.value = ticket;
  showForm.value = true;
};

/**
 * 关闭表单
 */
const closeForm = () => {
  showForm.value = false;
  editingTicket.value = null;
};

/**
 * 表单提交成功处理
 */
const handleFormSubmit = () => {
  closeForm();
  loadTickets();
  loadTicketStats();
};

/**
 * 删除工单
 */
const handleDelete = async (id: number) => {
  if (!confirm('确定要删除这个 Ticket 吗？')) return;

  try {
    await api.deleteTicket(id);
    loadTickets();
    loadTicketStats();
  } catch {
    alert('删除失败');
  }
};

/**
 * 切换工单状态
 */
const handleToggleStatus = async (id: number, status: string) => {
  try {
    const newStatus = status === 'completed' ? 'pending' : 'completed';
    await api.updateTicketStatus(id, newStatus);
    loadTickets();
    loadTicketStats();
  } catch {
    alert('状态更新失败');
  }
};

/**
 * 打开标签管理
 */
const openTagManager = () => {
  showTagManager.value = true;
};

/**
 * 关闭标签管理
 */
const closeTagManager = () => {
  showTagManager.value = false;
};

/**
 * 组件挂载时加载数据
 */
onMounted(() => {
  loadTickets();
  loadTags();
  loadTicketStats();
});
</script>

<style>
/* Apple 风格全局样式 */
:root {
  --color-primary: #0066cc;
  --color-primary-focus: #0071e3;
  --color-ink: #1d1d1f;
  --color-body: #1d1d1f;
  --color-body-muted: #666666;
  --color-canvas: #ffffff;
  --color-canvas-parchment: #f5f5f7;
  --color-surface-pearl: #fafafc;
  --color-divider: #e0e0e0;
  --color-hairline: #d2d2d7;

  --font-display: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
  --font-text: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif;

  --radius-pill: 9999px;
  --radius-lg: 18px;
  --radius-md: 11px;
  --radius-sm: 8px;

  --spacing-xs: 8px;
  --spacing-sm: 12px;
  --spacing-md: 17px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-text);
  font-size: 17px;
  line-height: 1.47;
  color: var(--color-body);
  background: var(--color-canvas-parchment);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  min-height: 100vh;
}

/* 全局导航栏 */
.global-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--color-divider);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-family: var(--font-display);
  font-size: 21px;
  font-weight: 600;
  color: var(--color-ink);
}

.brand-icon {
  color: var(--color-primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.nav-btn {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-body);
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: var(--color-canvas-parchment);
}

.nav-btn-primary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 11px 22px;
  font-size: 14px;
  font-weight: 400;
  color: white;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.nav-btn-primary:hover {
  background: var(--color-primary-focus);
}

.nav-btn-primary:active {
  transform: scale(0.98);
}

.btn-icon {
  font-size: 18px;
  font-weight: 300;
}

/* 主内容区 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-lg);
}

/* 搜索栏 */
.search-section {
  margin-bottom: var(--spacing-xl);
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: var(--spacing-md);
  width: 20px;
  height: 20px;
  color: var(--color-body-muted);
}

.search-input {
  width: 100%;
  padding: 14px var(--spacing-md) 14px 48px;
  font-size: 17px;
  font-family: var(--font-text);
  color: var(--color-body);
  background: var(--color-canvas);
  border: 1px solid var(--color-hairline);
  border-radius: var(--radius-pill);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1);
}

.search-input::placeholder {
  color: var(--color-body-muted);
}

/* 状态筛选 */
.status-section {
  margin-bottom: var(--spacing-xl);
}

.status-tabs {
  display: flex;
  gap: var(--spacing-sm);
  padding: 6px;
  background: var(--color-canvas);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-divider);
}

.status-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-body-muted);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.status-tab:hover {
  color: var(--color-body);
  background: var(--color-canvas-parchment);
}

.status-tab.active {
  color: var(--color-body);
  background: var(--color-canvas-parchment);
  font-weight: 500;
}

.tab-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.tab-dot.pending {
  background: #ff9500;
}

.tab-dot.completed {
  background: #34c759;
}

.tab-dot.all {
  background: var(--color-body-muted);
}

.tab-count {
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-body-muted);
  background: var(--color-canvas-parchment);
  border-radius: var(--radius-pill);
}

/* Ticket 列表区 */
.tickets-section {
  background: var(--color-canvas);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-divider);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--color-divider);
}

.section-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 600;
  color: var(--color-ink);
  letter-spacing: -0.021em;
}

.section-count {
  font-size: 14px;
  color: var(--color-body-muted);
}

/* 分页 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg) var(--spacing-xl);
  border-top: 1px solid var(--color-divider);
  background: var(--color-surface-pearl);
}

.pagination-info {
  font-size: 14px;
  color: var(--color-body-muted);
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.pagination-btn {
  padding: 8px 16px;
  font-size: 14px;
  color: var(--color-primary);
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(0, 102, 204, 0.1);
}

.pagination-btn:disabled {
  color: var(--color-body-muted);
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-number {
  min-width: 36px;
  padding: 8px;
  font-size: 14px;
  color: var(--color-body);
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.page-number:hover {
  background: var(--color-canvas-parchment);
}

.page-number.active {
  color: white;
  background: var(--color-primary);
}

.page-size-selector select {
  padding: 8px 12px;
  font-size: 14px;
  color: var(--color-body);
  background: var(--color-canvas);
  border: 1px solid var(--color-hairline);
  border-radius: var(--radius-sm);
  cursor: pointer;
  outline: none;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xxl) var(--spacing-xl);
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-lg);
}

.empty-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--spacing-sm);
}

.empty-desc {
  font-size: 17px;
  color: var(--color-body-muted);
  margin-bottom: var(--spacing-xl);
}

.empty-btn {
  padding: 14px 28px;
  font-size: 17px;
  font-weight: 400;
  color: white;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.empty-btn:hover {
  background: var(--color-primary-focus);
}

.empty-btn:active {
  transform: scale(0.98);
}

/* 响应式 */
@media (max-width: 768px) {
  .nav-content {
    padding: 0 var(--spacing-md);
  }

  .nav-brand {
    font-size: 18px;
  }

  .nav-btn {
    display: none;
  }

  .main-content {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .section-title {
    font-size: 24px;
  }

  .pagination {
    flex-direction: column;
    gap: var(--spacing-md);
  }
}
</style>
