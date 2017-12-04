import fetch from '@/utils/fetch'

export function play(logfloder) {
  return fetch({
    url: '/play',
    method: 'get',
    params: { logfloder }
  })
}
