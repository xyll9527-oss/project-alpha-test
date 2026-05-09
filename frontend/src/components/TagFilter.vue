<template>
  <section class="tag-filter-section">
    <div class="tag-filter-container">
      <span class="filter-label">标签筛选</span>
      <div class="tag-list">
        <button
          class="tag-btn"
          :class="{ active: selectedTag === null }"
          @click="selectTag(null)"
        >
          <span class="tag-dot all"></span>
          <span class="tag-name">全部</span>
        </button>
        
        <button
          v-for="tag in tags"
          :key="tag.id"
          class="tag-btn"
          :class="{ active: selectedTag === tag.id }"
          :style="getTagStyle(tag)"
          @click="selectTag(tag.id)"
        >
          <span class="tag-dot" :style="{ backgroundColor: tag.color }"></span>
          <span class="tag-name">{{ tag.name }}</span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Tag } from '@/types';

const props = defineProps<{
  tags: Tag[];
  selectedTag: number | null;
}>();

const emit = defineEmits<{
  (e: 'select', tagId: number | null): void;
}>();

/**
 * 获取标签样式
 */
const getTagStyle = (tag: Tag) => {
  const isSelected = props.selectedTag === tag.id;
  return {
    backgroundColor: isSelected ? tag.color : tag.color + '15',
    color: isSelected ? '#fff' : tag.color,
    borderColor: tag.color + '40'
  };
};

/**
 * 选择标签
 */
const selectTag = (tagId: number | null) => {
  emit('select', tagId);
};
</script>

<style scoped>
.tag-filter-section {
  margin-bottom: var(--spacing-xl);
}

.tag-filter-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.filter-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-body-muted);
  flex-shrink: 0;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  background: var(--color-canvas);
  border: 1px solid var(--color-hairline);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-btn:hover {
  background: var(--color-canvas-parchment);
}

.tag-btn.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.tag-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.tag-dot.all {
  background: var(--color-body-muted);
}

.tag-name {
  white-space: nowrap;
}

/* 响应式 */
@media (max-width: 768px) {
  .tag-filter-container {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .tag-list {
    width: 100%;
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 4px;
    -webkit-overflow-scrolling: touch;
  }

  .tag-list::-webkit-scrollbar {
    display: none;
  }
}
</style>
